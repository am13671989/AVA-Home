package com.ava.home

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.ava.home.data.AvaHomeScreen
import com.ava.home.data.PredictionResult
import com.ava.home.data.PropertyInput
import com.ava.home.data.SavedPrediction
import com.ava.home.data.appLanguages
import com.ava.home.data.predictPropertyPrice
import com.ava.home.data.tr
import com.ava.home.network.AvaHomeBackendClient
import com.ava.home.storage.PredictionStorage
import com.ava.home.ui.components.AvaBottomBar
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.screens.PropertyFormScreen
import com.ava.home.ui.screens.ResultScreen
import com.ava.home.ui.screens.SavedScreen
import com.ava.home.ui.screens.SettingsScreen
import com.ava.home.ui.screens.WelcomeScreen
import com.ava.home.ui.theme.AvaHomeTheme
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AvaHomeTheme {
                AvaHomeApp()
            }
        }
    }
}

@Composable
fun AvaHomeApp() {
    val context = LocalContext.current
    val storage = remember { PredictionStorage(context) }
    var screen by remember { mutableStateOf(AvaHomeScreen.Welcome) }
    var input by remember { mutableStateOf(PropertyInput()) }
    var result by remember { mutableStateOf<PredictionResult?>(null) }
    var savedPredictions by remember { mutableStateOf(emptyList<SavedPrediction>()) }
    var language by remember { mutableStateOf(appLanguages.first()) }
    var menuOpen by remember { mutableStateOf(false) }
    var quickFeedback by remember { mutableStateOf("") }
    var feedbackSaved by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        savedPredictions = storage.load()
    }

    fun calculate() {
        screen = AvaHomeScreen.Result
        result = null
        Thread {
            val prediction = AvaHomeBackendClient.predict(input)
                ?: predictPropertyPrice(input)
            Handler(Looper.getMainLooper()).post {
                result = prediction
            }
        }.start()
    }

    fun saveCurrentPrediction() {
        val current = result ?: return
        val surface = input.surface.toIntOrNull() ?: 80
        val date = SimpleDateFormat("dd MMM yyyy", Locale.getDefault()).format(Date())
        storage.save(
            SavedPrediction(
                id = System.currentTimeMillis(),
                title = "${input.city} property estimate",
                city = input.city,
                surface = surface,
                predictedPrice = current.predictedPrice,
                createdAt = date
            )
        )
        savedPredictions = storage.load()
        screen = AvaHomeScreen.Saved
    }

    Scaffold(
        bottomBar = {
            AvaBottomBar(current = screen, languageCode = language.code) { destination ->
                screen = destination
            }
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when (screen) {
                AvaHomeScreen.Welcome -> WelcomeScreen(
                    language = language,
                    onLanguageChange = { language = it },
                    onStart = { screen = AvaHomeScreen.Form }
                )
                AvaHomeScreen.Form -> PropertyFormScreen(
                    input = input,
                    languageCode = language.code,
                    onInputChange = { input = it },
                    onPredict = ::calculate
                )
                AvaHomeScreen.Result -> ResultScreen(
                    input = input,
                    result = result,
                    languageCode = language.code,
                    onSave = ::saveCurrentPrediction,
                    onEdit = { screen = AvaHomeScreen.Form }
                )
                AvaHomeScreen.Saved -> SavedScreen(
                    predictions = savedPredictions,
                    languageCode = language.code,
                    onNewPrediction = { screen = AvaHomeScreen.Form },
                    onClear = {
                        storage.clear()
                        savedPredictions = emptyList()
                    }
                )
                AvaHomeScreen.Settings -> SettingsScreen(languageCode = language.code)
            }

            IconButton(
                onClick = { menuOpen = true },
                modifier = Modifier
                    .align(Alignment.TopStart)
                    .padding(8.dp)
            ) {
                Icon(Icons.Default.Menu, contentDescription = tr(language.code, "menu"))
            }

            if (menuOpen) {
                SectionCard(
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .padding(start = 14.dp, top = 56.dp, end = 14.dp)
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Box(modifier = Modifier.fillMaxWidth()) {
                            Text(
                                tr(language.code, "feedback"),
                                fontWeight = FontWeight.Black,
                                modifier = Modifier.align(Alignment.CenterStart)
                            )
                            IconButton(
                                onClick = { menuOpen = false },
                                modifier = Modifier.align(Alignment.CenterEnd)
                            ) {
                                Icon(Icons.Default.Close, contentDescription = tr(language.code, "close"))
                            }
                        }
                        Text(tr(language.code, "feedback_body"))
                        OutlinedTextField(
                            value = quickFeedback,
                            onValueChange = {
                                quickFeedback = it
                                feedbackSaved = false
                            },
                            label = { Text(tr(language.code, "feedback_placeholder")) },
                            modifier = Modifier.fillMaxWidth()
                        )
                        PrimaryButton(tr(language.code, "send_feedback")) {
                            feedbackSaved = quickFeedback.isNotBlank()
                        }
                        if (feedbackSaved) {
                            Text(tr(language.code, "feedback_saved"))
                        }
                    }
                }
            }
        }
    }
}

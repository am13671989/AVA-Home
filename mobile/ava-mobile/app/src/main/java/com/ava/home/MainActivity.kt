package com.ava.home

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import com.ava.home.data.AvaHomeScreen
import com.ava.home.data.PredictionResult
import com.ava.home.data.PropertyInput
import com.ava.home.data.SavedPrediction
import com.ava.home.data.predictPropertyPrice
import com.ava.home.storage.PredictionStorage
import com.ava.home.ui.components.AvaBottomBar
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

    LaunchedEffect(Unit) {
        savedPredictions = storage.load()
    }

    fun calculate() {
        result = predictPropertyPrice(input)
        screen = AvaHomeScreen.Result
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
            AvaBottomBar(current = screen) { destination ->
                screen = destination
            }
        }
    ) { padding ->
        androidx.compose.foundation.layout.Box(modifier = Modifier.padding(padding)) {
            when (screen) {
                AvaHomeScreen.Welcome -> WelcomeScreen(onStart = { screen = AvaHomeScreen.Form })
                AvaHomeScreen.Form -> PropertyFormScreen(
                    input = input,
                    onInputChange = { input = it },
                    onPredict = ::calculate
                )
                AvaHomeScreen.Result -> ResultScreen(
                    input = input,
                    result = result,
                    onSave = ::saveCurrentPrediction,
                    onEdit = { screen = AvaHomeScreen.Form }
                )
                AvaHomeScreen.Saved -> SavedScreen(
                    predictions = savedPredictions,
                    onNewPrediction = { screen = AvaHomeScreen.Form },
                    onClear = {
                        storage.clear()
                        savedPredictions = emptyList()
                    }
                )
                AvaHomeScreen.Settings -> SettingsScreen()
            }
        }
    }
}

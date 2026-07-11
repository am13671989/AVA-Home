package com.ava.home.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Api
import androidx.compose.material.icons.filled.Cloud
import androidx.compose.material.icons.filled.Feedback
import androidx.compose.material.icons.filled.Storage
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.data.tr
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.Slate

@Composable
fun SettingsScreen(languageCode: String) {
    var feedback by remember { mutableStateOf("") }
    var saved by remember { mutableStateOf(false) }
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(tr(languageCode, "project_settings"), fontSize = 30.sp, fontWeight = FontWeight.Black)
        Text(tr(languageCode, "settings_intro"), color = Slate)

        SettingsCard(tr(languageCode, "api_target"), tr(languageCode, "api_target_body"), Icons.Default.Api)
        SettingsCard(tr(languageCode, "storage"), tr(languageCode, "storage_body"), Icons.Default.Storage)
        SettingsCard(tr(languageCode, "deployment"), tr(languageCode, "deployment_body"), Icons.Default.Cloud)
        SectionCard {
            Icon(Icons.Default.Feedback, contentDescription = tr(languageCode, "feedback"), tint = Mint)
            Text(tr(languageCode, "feedback"), fontWeight = FontWeight.Black, fontSize = 18.sp)
            Text(tr(languageCode, "feedback_body"), color = Slate)
            OutlinedTextField(
                value = feedback,
                onValueChange = {
                    feedback = it
                    saved = false
                },
                label = { Text(tr(languageCode, "feedback_placeholder")) }
            )
            PrimaryButton(tr(languageCode, "send_feedback")) { saved = feedback.isNotBlank() }
            if (saved) {
                Text(tr(languageCode, "feedback_saved"), color = Mint)
            }
        }
    }
}

@Composable
private fun SettingsCard(title: String, body: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    SectionCard {
        Icon(icon, contentDescription = title, tint = Mint)
        Text(title, fontWeight = FontWeight.Black, fontSize = 18.sp)
        Text(body, color = Slate)
    }
}

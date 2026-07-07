package com.ava.home.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Api
import androidx.compose.material.icons.filled.Cloud
import androidx.compose.material.icons.filled.Storage
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.Slate

@Composable
fun SettingsScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Project settings", fontSize = 30.sp, fontWeight = FontWeight.Black)
        Text("Current app mode and next backend connection steps.", color = Slate)

        SettingsCard("API target", "FastAPI endpoint: /api/home/predict", Icons.Default.Api)
        SettingsCard("Storage", "Predictions are saved locally in this first mobile version.", Icons.Default.Storage)
        SettingsCard("Deployment", "Prepared for GitHub, Docker, Hetzner, PostgreSQL, and ML model integration.", Icons.Default.Cloud)
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

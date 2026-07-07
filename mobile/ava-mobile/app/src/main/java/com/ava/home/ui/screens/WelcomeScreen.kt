package com.ava.home.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.HomeWork
import androidx.compose.material.icons.filled.Insights
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.ui.components.HeroHeader
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.Slate

@Composable
fun WelcomeScreen(onStart: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        HeroHeader(
            title = "Home price estimation",
            subtitle = "Estimate a property's market value, compare signals, and save predictions for later decisions."
        )

        SectionCard {
            FeatureLine("Enter property details", "Surface, rooms, city, year, condition, and features.", Icons.Default.HomeWork)
            FeatureLine("Get an instant estimate", "The first version uses a local model-style estimator.", Icons.Default.Insights)
            FeatureLine("Save your predictions", "Keep a lightweight history before backend sync is added.", Icons.Default.Save)
        }

        Spacer(modifier = Modifier.weight(1f))
        PrimaryButton(text = "Start property estimate", onClick = onStart)
    }
}

@Composable
private fun FeatureLine(title: String, detail: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    androidx.compose.foundation.layout.Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        Icon(icon, contentDescription = title, tint = Mint)
        Column {
            Text(title, fontWeight = FontWeight.Black, fontSize = 16.sp)
            Text(detail, color = Slate, lineHeight = 20.sp)
        }
    }
}

package com.ava.home.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.data.SavedPrediction
import com.ava.home.data.formatEuro
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.Slate

@Composable
fun SavedScreen(
    predictions: List<SavedPrediction>,
    onNewPrediction: () -> Unit,
    onClear: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Saved predictions", fontSize = 30.sp, fontWeight = FontWeight.Black)
        Text("Your latest local estimates. Backend sync will come in the next version.", color = Slate)

        if (predictions.isEmpty()) {
            SectionCard {
                Icon(Icons.Default.Bookmark, contentDescription = "Saved", tint = Mint)
                Text("No saved predictions yet", fontWeight = FontWeight.Black)
                Text("Create a first home estimate and save it here.", color = Slate)
            }
            PrimaryButton("Create prediction", onClick = onNewPrediction)
        } else {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.weight(1f)) {
                items(predictions) { item ->
                    SectionCard {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(item.title, fontWeight = FontWeight.Black)
                                Text("${item.city} · ${item.surface} m2 · ${item.createdAt}", color = Slate)
                            }
                            Text(formatEuro(item.predictedPrice), fontWeight = FontWeight.Black, color = Mint)
                        }
                    }
                }
            }
            PrimaryButton("New prediction", onClick = onNewPrediction)
            PrimaryButton("Clear saved predictions", onClick = onClear)
        }
    }
}

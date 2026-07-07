package com.ava.home.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Apartment
import androidx.compose.material.icons.filled.LocationCity
import androidx.compose.material.icons.filled.SquareFoot
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.data.PredictionResult
import com.ava.home.data.PropertyInput
import com.ava.home.data.formatEuro
import com.ava.home.ui.components.ConfidenceGauge
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.Slate

@Composable
fun ResultScreen(
    input: PropertyInput,
    result: PredictionResult?,
    onSave: () -> Unit,
    onEdit: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Estimated market value", fontSize = 28.sp, fontWeight = FontWeight.Black)

        if (result == null) {
            Text("No prediction yet. Go to the form and calculate a first estimate.", color = Slate)
            PrimaryButton("Open property form", onClick = onEdit)
            return@Column
        }

        SectionCard {
            Text(formatEuro(result.predictedPrice), fontSize = 36.sp, fontWeight = FontWeight.Black, color = Mint)
            Text(result.summary, color = Slate)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                ConfidenceGauge(result.confidence, "Confidence")
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    InfoLine(Icons.Default.LocationCity, result.city)
                    InfoLine(Icons.Default.SquareFoot, "${input.surface.ifBlank { "80" }} m2")
                    InfoLine(Icons.Default.Apartment, "${formatEuro(result.pricePerSquareMeter)} / m2")
                }
            }
        }

        SectionCard {
            Text("Decision notes", fontWeight = FontWeight.Black)
            Text("This first mobile version mirrors the PDF MVP: property data in, estimated price out, prediction saved locally.", color = Slate)
            Text("Next professional step: connect this screen to FastAPI /api/home/predict and store results in PostgreSQL.", color = Slate)
        }

        PrimaryButton("Save prediction", onClick = onSave)
        PrimaryButton("Edit property details", onClick = onEdit)
    }
}

@Composable
private fun InfoLine(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, contentDescription = text, tint = Mint)
        Text(text, fontWeight = FontWeight.Bold)
    }
}

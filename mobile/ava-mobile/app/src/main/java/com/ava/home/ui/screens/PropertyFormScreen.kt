package com.ava.home.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.data.PropertyInput
import com.ava.home.data.propertyConditions
import com.ava.home.data.supportedCities
import com.ava.home.ui.components.ChoiceField
import com.ava.home.ui.components.FeatureChip
import com.ava.home.ui.components.NumberField
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Slate

@Composable
fun PropertyFormScreen(
    input: PropertyInput,
    onInputChange: (PropertyInput) -> Unit,
    onPredict: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Property details", fontSize = 30.sp, fontWeight = FontWeight.Black)
        Text("Fill the essential fields for the first Ava Home price estimation.", color = Slate)

        SectionCard {
            ChoiceField("City", input.city, supportedCities) { onInputChange(input.copy(city = it)) }
            NumberField("Postal code", input.postalCode, { onInputChange(input.copy(postalCode = it)) })
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                NumberField("Surface m2", input.surface, { onInputChange(input.copy(surface = it)) }, Modifier.weight(1f))
                NumberField("Rooms", input.rooms, { onInputChange(input.copy(rooms = it)) }, Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                NumberField("Bedrooms", input.bedrooms, { onInputChange(input.copy(bedrooms = it)) }, Modifier.weight(1f))
                NumberField("Year", input.year, { onInputChange(input.copy(year = it)) }, Modifier.weight(1f))
            }
            ChoiceField("Condition", input.condition, propertyConditions) { onInputChange(input.copy(condition = it)) }
        }

        SectionCard {
            Text("Property features", fontWeight = FontWeight.Black)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                FeatureChip("Garage", input.garage) { onInputChange(input.copy(garage = !input.garage)) }
                FeatureChip("Balcony", input.balcony) { onInputChange(input.copy(balcony = !input.balcony)) }
                FeatureChip("Garden", input.garden) { onInputChange(input.copy(garden = !input.garden)) }
            }
        }

        PrimaryButton("Calculate estimated price", onClick = onPredict)
    }
}

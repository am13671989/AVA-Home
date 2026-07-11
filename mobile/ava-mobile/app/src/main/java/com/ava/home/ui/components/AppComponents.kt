package com.ava.home.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.QueryStats
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.data.AvaHomeScreen
import com.ava.home.data.tr
import com.ava.home.ui.theme.Amber
import com.ava.home.ui.theme.CardWhite
import com.ava.home.ui.theme.Coral
import com.ava.home.ui.theme.Ink
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.MintDark
import com.ava.home.ui.theme.Slate

@Composable
fun SectionCard(
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = CardWhite),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            content = content
        )
    }
}

@Composable
fun PrimaryButton(
    text: String,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = modifier
            .fillMaxWidth()
            .height(54.dp),
        shape = RoundedCornerShape(18.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Mint)
    ) {
        Text(text = text, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun NumberField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    OutlinedTextField(
        value = value,
        onValueChange = { onValueChange(it.filter { char -> char.isDigit() }) },
        label = { Text(label) },
        singleLine = true,
        modifier = modifier.fillMaxWidth()
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChoiceField(
    label: String,
    value: String,
    options: List<String>,
    onSelected: (String) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
        OutlinedTextField(
            value = value,
            onValueChange = {},
            readOnly = true,
            label = { Text(label) },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            modifier = Modifier
                .menuAnchor()
                .fillMaxWidth()
        )
        ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { option ->
                DropdownMenuItem(
                    text = { Text(option.replaceFirstChar { it.uppercase() }) },
                    onClick = {
                        onSelected(option)
                        expanded = false
                    }
                )
            }
        }
    }
}

@Composable
fun FeatureChip(
    label: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        shape = RoundedCornerShape(16.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = if (selected) Mint else CardWhite,
            contentColor = if (selected) CardWhite else Ink
        )
    ) {
        Text(label, fontWeight = FontWeight.Bold)
    }
}

@Composable
fun ConfidenceGauge(value: Float, label: String) {
    val color = when {
        value >= 0.72f -> Mint
        value >= 0.6f -> Amber
        else -> Coral
    }
    Box(contentAlignment = Alignment.Center, modifier = Modifier.size(116.dp)) {
        Canvas(modifier = Modifier.size(116.dp)) {
            drawArc(
                color = Slate.copy(alpha = 0.18f),
                startAngle = 150f,
                sweepAngle = 240f,
                useCenter = false,
                style = Stroke(width = 12.dp.toPx(), cap = StrokeCap.Round),
                size = Size(size.width - 16.dp.toPx(), size.height - 16.dp.toPx()),
                topLeft = Offset(8.dp.toPx(), 8.dp.toPx())
            )
            drawArc(
                color = color,
                startAngle = 150f,
                sweepAngle = 240f * value.coerceIn(0f, 1f),
                useCenter = false,
                style = Stroke(width = 12.dp.toPx(), cap = StrokeCap.Round),
                size = Size(size.width - 16.dp.toPx(), size.height - 16.dp.toPx()),
                topLeft = Offset(8.dp.toPx(), 8.dp.toPx())
            )
        }
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("${(value * 100).toInt()}%", color = Ink, fontWeight = FontWeight.Black)
            Text(label, color = Slate, fontSize = 12.sp)
        }
    }
}

@Composable
fun AvaBottomBar(current: AvaHomeScreen, languageCode: String, onNavigate: (AvaHomeScreen) -> Unit) {
    val items = listOf(
        NavItem(AvaHomeScreen.Welcome, tr(languageCode, "home"), Icons.Default.Home),
        NavItem(AvaHomeScreen.Form, tr(languageCode, "predict"), Icons.Default.QueryStats),
        NavItem(AvaHomeScreen.Saved, tr(languageCode, "saved"), Icons.Default.Bookmark)
    )
    NavigationBar(containerColor = CardWhite) {
        items.forEach { item ->
            NavigationBarItem(
                selected = current == item.screen,
                onClick = { onNavigate(item.screen) },
                icon = { Icon(item.icon, contentDescription = item.label) },
                label = { Text(item.label) }
            )
        }
    }
}

@Composable
fun HeroHeader(title: String, subtitle: String) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(MintDark, RoundedCornerShape(28.dp))
            .padding(22.dp)
    ) {
        Text("AVA", color = Mint, fontSize = 42.sp, fontWeight = FontWeight.Black)
        Spacer(Modifier.height(10.dp))
        Text(title, color = CardWhite, fontSize = 24.sp, fontWeight = FontWeight.Black)
        Text(subtitle, color = CardWhite.copy(alpha = 0.82f), lineHeight = 22.sp)
    }
}

private data class NavItem(
    val screen: AvaHomeScreen,
    val label: String,
    val icon: ImageVector
)

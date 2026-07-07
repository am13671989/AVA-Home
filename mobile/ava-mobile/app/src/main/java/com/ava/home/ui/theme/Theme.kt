package com.ava.home.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val AvaHomeColors = lightColorScheme(
    primary = Mint,
    secondary = Amber,
    tertiary = Coral,
    background = SkySoft,
    surface = CardWhite,
    onPrimary = CardWhite,
    onSurface = Ink
)

@Composable
fun AvaHomeTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = AvaHomeColors,
        content = content
    )
}

package com.ava.home.data

import kotlin.math.roundToInt

fun predictPropertyPrice(input: PropertyInput): PredictionResult {
    val surface = input.surface.toIntOrNull()?.coerceAtLeast(10) ?: 80
    val rooms = input.rooms.toIntOrNull()?.coerceAtLeast(1) ?: 3
    val bedrooms = input.bedrooms.toIntOrNull()?.coerceAtLeast(0) ?: 2
    val year = input.year.toIntOrNull() ?: 2005
    val basePrice = cityPricePerSquareMeter[input.city] ?: 4500

    val conditionFactor = when (input.condition) {
        "new" -> 1.16
        "excellent" -> 1.10
        "good" -> 1.0
        else -> 0.86
    }
    val featureBonus = listOf(input.garage, input.balcony, input.garden).count { it } * 9500
    val roomBonus = (rooms * 3200) + (bedrooms * 1800)
    val ageFactor = when {
        year >= 2020 -> 1.07
        year >= 2010 -> 1.03
        year >= 1990 -> 0.98
        else -> 0.92
    }

    val predicted = ((surface * basePrice * conditionFactor * ageFactor) + featureBonus + roomBonus).roundToInt()
    val confidence = when {
        input.surface.isBlank() || input.rooms.isBlank() -> 0.54f
        input.postalCode.isBlank() -> 0.68f
        else -> 0.76f
    }

    return PredictionResult(
        predictedPrice = predicted,
        confidence = confidence,
        pricePerSquareMeter = predicted / surface,
        city = input.city,
        summary = "Based on surface, rooms, location, features, year, and condition."
    )
}

fun formatEuro(value: Int): String = "EUR %,d".format(value).replace(",", " ")

package com.ava.home.data

data class PropertyInput(
    val surface: String = "",
    val rooms: String = "",
    val bedrooms: String = "",
    val city: String = "Lyon",
    val postalCode: String = "",
    val garage: Boolean = false,
    val balcony: Boolean = false,
    val garden: Boolean = false,
    val year: String = "",
    val condition: String = "good"
)

data class PredictionResult(
    val predictedPrice: Int,
    val confidence: Float,
    val pricePerSquareMeter: Int,
    val city: String,
    val summary: String,
    val modelType: String = "Local estimator",
    val dataScope: String = "mobile fallback",
    val priceRangeLow: Int? = null,
    val priceRangeHigh: Int? = null,
    val source: String = "local"
)

data class SavedPrediction(
    val id: Long,
    val title: String,
    val city: String,
    val surface: Int,
    val predictedPrice: Int,
    val createdAt: String
)

enum class AvaHomeScreen {
    Welcome,
    Form,
    Result,
    Saved
}

package com.ava.home.data

val supportedCountries = listOf("France", "Spain")

val citiesByCountry = mapOf(
    "France" to listOf(
        "Paris", "Lyon", "Marseille", "Toulouse", "Nice",
        "Bordeaux", "Lille", "Nantes", "Montpellier", "Rennes"
    ),
    "Spain" to listOf("Barcelona", "Madrid", "Seville", "Valencia")
)

fun supportedCities(country: String): List<String> = citiesByCountry[country].orEmpty()

val propertyConditions = listOf("new", "excellent", "good", "renovation")

// Used only by the offline mobile fallback when the country API is unavailable.
val cityPricePerSquareMeter = mapOf(
    "Paris" to 9_500, "Lyon" to 4_200, "Marseille" to 3_400,
    "Toulouse" to 3_350, "Nice" to 4_650, "Bordeaux" to 4_400,
    "Lille" to 3_550, "Nantes" to 3_600, "Montpellier" to 3_450,
    "Rennes" to 3_750, "Barcelona" to 5_100, "Madrid" to 4_700,
    "Seville" to 3_000, "Valencia" to 3_200,
)

package com.ava.home.network

import com.ava.home.data.PredictionResult
import com.ava.home.data.PropertyInput
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import kotlin.math.roundToInt

object AvaHomeBackendClient {
    private const val BASE_URL = "http://10.0.2.2:8000"

    fun predict(input: PropertyInput): PredictionResult? {
        return try {
            val connection = (URL("$BASE_URL/api/home/predict").openConnection() as HttpURLConnection).apply {
                requestMethod = "POST"
                connectTimeout = 5000
                readTimeout = 15000
                doOutput = true
                setRequestProperty("Content-Type", "application/json")
            }

            val body = JSONObject()
                .put("surface", input.surface.toDoubleOrNull() ?: 80.0)
                .put("rooms", input.rooms.toIntOrNull() ?: 3)
                .put("bedrooms", input.bedrooms.toIntOrNull() ?: 2)
                .put("city", input.city)
                .put("postal_code", input.postalCode)
                .put("garage", if (input.garage) 1 else 0)
                .put("balcony", if (input.balcony) 1 else 0)
                .put("garden", if (input.garden) 1 else 0)
                .put("year", input.year.toIntOrNull() ?: 2024)
                .put("condition", input.condition)

            OutputStreamWriter(connection.outputStream).use { writer ->
                writer.write(body.toString())
            }

            if (connection.responseCode !in 200..299) {
                connection.disconnect()
                return null
            }

            val response = connection.inputStream.bufferedReader().use { it.readText() }
            connection.disconnect()
            val json = JSONObject(response)
            val predicted = json.getDouble("predicted_price").roundToInt()
            val pricePerM2 = json.optDouble("estimated_price_per_m2", 0.0).roundToInt()

            PredictionResult(
                predictedPrice = predicted,
                confidence = json.optDouble("confidence_score", 0.0).toFloat(),
                pricePerSquareMeter = pricePerM2,
                city = input.city,
                summary = json.optString("message", "Prediction completed with backend model."),
                modelType = json.optString("model_type", "RandomForestRegressor"),
                dataScope = json.optString("data_scope", "backend model"),
                priceRangeLow = json.optDouble("price_range_low", 0.0).roundToInt().takeIf { it > 0 },
                priceRangeHigh = json.optDouble("price_range_high", 0.0).roundToInt().takeIf { it > 0 },
                source = "FastAPI backend"
            )
        } catch (_: Exception) {
            null
        }
    }
}

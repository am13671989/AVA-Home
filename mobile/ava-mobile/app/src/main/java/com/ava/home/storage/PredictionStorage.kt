package com.ava.home.storage

import android.content.Context
import com.ava.home.data.SavedPrediction

class PredictionStorage(context: Context) {
    private val prefs = context.getSharedPreferences("ava_home_predictions", Context.MODE_PRIVATE)

    fun save(prediction: SavedPrediction) {
        val current = load().filterNot { it.id == prediction.id }
        val encoded = (listOf(prediction) + current)
            .take(20)
            .joinToString("\n") { item ->
                listOf(
                    item.id,
                    item.title,
                    item.city,
                    item.surface,
                    item.predictedPrice,
                    item.createdAt
                ).joinToString("|")
            }
        prefs.edit().putString("items", encoded).apply()
    }

    fun load(): List<SavedPrediction> {
        return prefs.getString("items", null)
            ?.lineSequence()
            ?.mapNotNull { line ->
                val parts = line.split("|")
                if (parts.size != 6) return@mapNotNull null
                SavedPrediction(
                    id = parts[0].toLongOrNull() ?: return@mapNotNull null,
                    title = parts[1],
                    city = parts[2],
                    surface = parts[3].toIntOrNull() ?: 0,
                    predictedPrice = parts[4].toIntOrNull() ?: 0,
                    createdAt = parts[5]
                )
            }
            ?.toList()
            ?: emptyList()
    }

    fun clear() {
        prefs.edit().remove("items").apply()
    }
}

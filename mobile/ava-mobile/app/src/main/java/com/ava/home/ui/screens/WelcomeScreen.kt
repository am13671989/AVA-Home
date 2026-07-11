package com.ava.home.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.HomeWork
import androidx.compose.material.icons.filled.Insights
import androidx.compose.material.icons.filled.Save
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ava.home.R
import com.ava.home.data.AppLanguage
import com.ava.home.data.appLanguages
import com.ava.home.data.tr
import com.ava.home.ui.components.ChoiceField
import com.ava.home.ui.components.HeroHeader
import com.ava.home.ui.components.PrimaryButton
import com.ava.home.ui.components.SectionCard
import com.ava.home.ui.theme.Mint
import com.ava.home.ui.theme.Slate

@Composable
fun WelcomeScreen(
    language: AppLanguage,
    onLanguageChange: (AppLanguage) -> Unit,
    onStart: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        SectionCard {
            Image(
                painter = painterResource(id = R.drawable.ava_home_brand),
                contentDescription = "Ava Home logo",
                modifier = Modifier
                    .fillMaxWidth()
                    .height(190.dp),
                contentScale = ContentScale.Fit
            )
        }

        HeroHeader(
            title = tr(language.code, "welcome_title"),
            subtitle = tr(language.code, "welcome_subtitle")
        )

        SectionCard {
            ChoiceField(
                label = tr(language.code, "language"),
                value = language.label,
                options = appLanguages.map { it.label },
                onSelected = { selected ->
                    appLanguages.firstOrNull { it.label == selected }?.let(onLanguageChange)
                }
            )
        }

        SectionCard {
            FeatureLine(tr(language.code, "feature_details"), tr(language.code, "feature_details_body"), Icons.Default.HomeWork)
            FeatureLine(tr(language.code, "feature_model"), tr(language.code, "feature_model_body"), Icons.Default.Insights)
            FeatureLine(tr(language.code, "feature_save"), tr(language.code, "feature_save_body"), Icons.Default.Save)
        }

        Spacer(modifier = Modifier.weight(1f))
        PrimaryButton(text = tr(language.code, "start"), onClick = onStart)
    }
}

@Composable
private fun FeatureLine(title: String, detail: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    androidx.compose.foundation.layout.Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        Icon(icon, contentDescription = title, tint = Mint)
        Column {
            Text(title, fontWeight = FontWeight.Black, fontSize = 16.sp)
            Text(detail, color = Slate, lineHeight = 20.sp)
        }
    }
}

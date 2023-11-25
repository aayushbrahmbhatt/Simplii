package com.bytes.a.half.simplii_android.composables

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.ExperimentalMaterialApi
import androidx.compose.material.ListItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.bytes.a.half.simplii_android.models.Task

@OptIn(ExperimentalMaterialApi::class)
@Composable
fun TaskScreen(tasks: List<Task>) {
    Scaffold {
        LazyColumn(modifier = Modifier.padding(it)) {
            itemsIndexed(tasks) { index, item ->
                ListItem(text = {
                    Text(item.title)
                })
            }
        }
    }
}
package com.bytes.a.half.simplii_android.composables

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import com.bytes.a.half.simplii_android.R


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(onCreateNewTask: () -> Unit) {
    var tabIndex by remember { mutableIntStateOf(0) }
    Scaffold(topBar = {
        TopAppBar(title = { Text(text = stringResource(id = R.string.simplii)) })
    }, floatingActionButton = {
        FloatingActionButton(onClick = {
            onCreateNewTask()
        }) {
            Icon(
                Icons.Filled.Add, "",
                // If tint color is provided, it will override contentColor below
                tint = Color.White,
            )
        }
    }) {
        Column(modifier = Modifier.padding(it)) {
            val tabList = listOf(
                stringResource(id = R.string.todo),
                stringResource(id = R.string.in_progress),
                stringResource(id = R.string.done)
            )
            Column(modifier = Modifier.fillMaxWidth()) {
                TabRow(selectedTabIndex = tabIndex) {
                    tabList.forEachIndexed { index, title ->
                        Tab(text = { Text(title) },
                            selected = tabIndex == index,
                            onClick = { tabIndex = index }
                        )
                    }
                }
                when (tabIndex) {
                    0 -> TaskScreen()
                    1 -> TaskScreen()
                    2 -> TaskScreen()
                }
            }
        }
    }
}
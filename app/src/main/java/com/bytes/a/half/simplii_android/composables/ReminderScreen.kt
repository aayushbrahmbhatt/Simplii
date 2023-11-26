package com.bytes.a.half.simplii_android.composables

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.ContentAlpha
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.Done
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TimePicker
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberDatePickerState
import androidx.compose.material3.rememberTimePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.bytes.a.half.simplii_android.R
import com.bytes.a.half.simplii_android.SimpliiConstants
import java.util.Calendar
import java.util.Date


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReminderScreen(
    taskId: String,
    taskTitle: String,
    onClose: () -> Unit,
    onSetReminder: () -> Unit
) {
    var reminderDateString by remember {
        mutableStateOf("")
    }
    var reminderTimeString by remember {
        mutableStateOf("")
    }
    Scaffold(topBar = {
        TopAppBar(
            title = {
                Text(
                    text = stringResource(id = R.string.set_reminder),
                    fontSize = 20.sp,
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
            },
            navigationIcon = {
                IconButton(onClick = {
                    onClose()
                }) {
                    Icon(Icons.Filled.ArrowBack, contentDescription = null)
                }
            },
            actions = {
                IconButton(onClick = {

                }) {
                    Icon(Icons.Filled.Done, contentDescription = null)
                }
            },
            colors = TopAppBarDefaults.topAppBarColors(
                containerColor = Color.Blue,
                titleContentColor = Color.White,
                navigationIconContentColor = Color.White,
                actionIconContentColor = Color.White
            )
        )
    }) {
        val openDatePickerDialog = remember { mutableStateOf(false) }
        val openTimePickerDialog = remember { mutableStateOf(false) }
        LazyColumn(modifier = Modifier.padding(it)) {
            item {
                if (openDatePickerDialog.value) {
                    val datePickerState = rememberDatePickerState()
                    DatePickerDialog(onDismissRequest = {
                        openDatePickerDialog.value = false
                    }, confirmButton = {
                        TextButton(
                            onClick = {
                                openDatePickerDialog.value = false

                            }, enabled = true
                        ) {
                            Text("OK")
                        }
                    }, dismissButton = {
                        TextButton(onClick = {
                            openDatePickerDialog.value = false
                        }) {
                            Text("Cancel")
                        }
                    }) {
                        DatePicker(state = datePickerState)
                    }
                }
            }

            item {
                if (openTimePickerDialog.value) {
                    val timePickerState = rememberTimePickerState()
                    TimePickerDialog(
                        onCancel = { openTimePickerDialog.value = false },
                        onConfirm = {
                            val cal = Calendar.getInstance()
                            cal.set(Calendar.HOUR_OF_DAY, timePickerState.hour)
                            cal.set(Calendar.MINUTE, timePickerState.minute)
                            cal.isLenient = false
                            openTimePickerDialog.value = false
                        },
                    ) {
                        TimePicker(state = timePickerState)
                    }
                }
            }

            item {
                Column(modifier = Modifier.clickable {
                    openDatePickerDialog.value = true
                }) {
                    OutlinedTextField(value = reminderDateString, modifier = Modifier
                        .heightIn(50.dp)
                        .fillMaxWidth()
                        .padding(start = 16.dp, end = 16.dp, top = 16.dp),
                        enabled = false,
                        onValueChange = {

                        },
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedTextColor = Color.Black,
                            unfocusedTextColor = Color.Black,
                            focusedBorderColor = Color.Black,
                            unfocusedBorderColor = Color.Black,
                            cursorColor = Color.Black,
                            disabledTextColor = Color.Black,
                            disabledTrailingIconColor = Color.Black
                        ),
                        label = {
                            Text(
                                text = stringResource(id = R.string.reminder_date),
                                color = Color.Black.copy(alpha = ContentAlpha.medium)
                            )
                        },
                        trailingIcon = {
                            Icon(Icons.Filled.DateRange, "")
                        })
                }

            }

            item {
                Column(modifier = Modifier.clickable {
                    openTimePickerDialog.value = true
                }) {
                    OutlinedTextField(value = reminderTimeString, modifier = Modifier
                        .heightIn(50.dp)
                        .fillMaxWidth()
                        .padding(start = 16.dp, end = 16.dp, top = 16.dp),
                        enabled = false,
                        onValueChange = {

                        },
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedTextColor = Color.Black,
                            unfocusedTextColor = Color.Black,
                            focusedBorderColor = Color.Black,
                            unfocusedBorderColor = Color.Black,
                            cursorColor = Color.Black,
                            disabledTextColor = Color.Black,
                            disabledTrailingIconColor = Color.Black
                        ),
                        label = {
                            Text(
                                text = stringResource(id = R.string.reminder_time),
                                color = Color.Black.copy(alpha = ContentAlpha.medium)
                            )
                        },
                        trailingIcon = {
                            Icon(Icons.Filled.DateRange, "")
                        })
                }

            }
        }
    }
}
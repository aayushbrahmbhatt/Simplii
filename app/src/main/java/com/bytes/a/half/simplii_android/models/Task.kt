package com.bytes.a.half.simplii_android.models

import java.util.Date

data class Task(
    val title: String,
    val status: Int,
    val hours: Int,
    val startDate: Date,
    val dueDate: Date
)

package com.bytes.a.half.simplii_android

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.activity.compose.setContent

class ReminderActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val taskTitle = intent.getStringExtra(SimpliiConstants.KEY_TASK_TITLE)
        val taskId = intent.getStringExtra(SimpliiConstants.KEY_TASK_ID)
        setContent {

        }
    }
}
package com.bytes.a.half.simplii_android

import android.app.Activity
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.activity.compose.setContent
import com.bytes.a.half.simplii_android.SimpliiConstants.KEY_TASK_CATEGORY
import com.bytes.a.half.simplii_android.SimpliiConstants.KEY_TASK_END_DATE
import com.bytes.a.half.simplii_android.SimpliiConstants.KEY_TASK_HOURS
import com.bytes.a.half.simplii_android.SimpliiConstants.KEY_TASK_START_DATE
import com.bytes.a.half.simplii_android.SimpliiConstants.KEY_TASK_STATUS
import com.bytes.a.half.simplii_android.SimpliiConstants.KEY_TASK_TITLE
import com.bytes.a.half.simplii_android.composables.CreateTaskScreen

class CreateTaskActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CreateTaskScreen(onClose = {
                finish()
            }) { taskData ->
                val intent = Intent().apply {
                    putExtra(KEY_TASK_TITLE, taskData.title)
                    putExtra(KEY_TASK_START_DATE, taskData.startDate.time)
                    putExtra(KEY_TASK_END_DATE, taskData.dueDate.time)
                    putExtra(KEY_TASK_STATUS, taskData.status)
                    putExtra(KEY_TASK_CATEGORY, taskData.category)
                    putExtra(KEY_TASK_HOURS, taskData.hours)
                }
                setResult(Activity.RESULT_OK, intent)
                finish()
            }

        }
    }
    
}

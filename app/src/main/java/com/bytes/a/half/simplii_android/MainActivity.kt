package com.bytes.a.half.simplii_android

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.activity.compose.setContent
import com.bytes.a.half.simplii_android.composables.HomeScreen

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            HomeScreen {
                openCreateTask()
            }
        }
    }

    private fun openCreateTask() {
        val intent = Intent(this, CreateTaskActivity::class.java)
        startActivity(intent)
    }
}
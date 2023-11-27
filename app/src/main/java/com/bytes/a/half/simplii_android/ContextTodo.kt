package com.bytes.a.half.simplii_android

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember

class ContextTodo : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val response = remember {
                mutableStateOf("")
            }
            LaunchedEffect(Unit) {
                val chatGPTResponse = SimpliiUtils.queryChatGPT(
                    this@ContextTodo,
                    "What are the steps to create a HTML Page"
                )
                response.value = chatGPTResponse
                System.out.println(response)
            }

            Column {
                Text(response.value)
            }
        }
    }
}
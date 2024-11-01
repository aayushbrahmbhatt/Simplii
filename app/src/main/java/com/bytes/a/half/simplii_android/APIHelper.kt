package com.bytes.a.half.simplii_android

import com.bytes.a.half.simplii_android.APIConstants.BASE_URL
import com.bytes.a.half.simplii_android.models.Reminder
import com.bytes.a.half.simplii_android.models.Task
import com.bytes.a.half.simplii_android.utils.FirebaseUtils
import kotlinx.coroutines.tasks.await
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object APIHelper {

    fun createRetrofitInstance(): Retrofit {
        val httpClientBuilder = OkHttpClient.Builder().addInterceptor(Interceptor { chain ->
            val modifiedRequest = chain.request().newBuilder()
                .addHeader("Content-Type", "application/json").build()
            chain.proceed(modifiedRequest)
        })
        httpClientBuilder.readTimeout(60, TimeUnit.SECONDS)
        httpClientBuilder.connectTimeout(60, TimeUnit.SECONDS)
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .client(httpClientBuilder.build())
            .build()
    }

    fun saveTask(task: Task) {
        FirebaseUtils.auth.uid?.let { userId ->
            val taskReference = FirebaseUtils.database.child("tasks").child(userId).push()
            task.id = taskReference.key
            taskReference.updateChildren(mapOf(task.id!! to task))
        }
    }

    fun saveReminder(reminder: Reminder) {
        FirebaseUtils.auth.uid?.let { userId ->
            val reminderReference = FirebaseUtils.database.child("reminders").child(userId).push()
            reminder.id = reminderReference.key
            reminderReference.updateChildren(mapOf(reminder.id!! to reminder))
        }
    }

    fun modifyTaskStatus(task: Task) {
        FirebaseUtils.auth.uid?.let { userId ->
            FirebaseUtils.database.child("tasks").child(userId).updateChildren(mapOf(task.id!! to task))
        }
    }

    fun removeTask(task: Task) {
        FirebaseUtils.auth.uid?.let { userId ->
            task.id?.let {
                FirebaseUtils.database.child("tasks").child(userId).child(it).removeValue()
            }
        }
    }

    fun removeReminder(reminder: Reminder) {
        FirebaseUtils.auth.uid?.let { userId ->
            reminder.id?.let {
                FirebaseUtils.database.child("reminders").child(userId).child(it).removeValue()
            }
        }
    }

    suspend fun fetchTasks(): ArrayList<Task> {
        val taskList = ArrayList<Task>()
        FirebaseUtils.auth.uid?.let { userId ->
            val snapshot = FirebaseUtils.database.child("tasks").child(userId).get().await()
            for (child in snapshot.children) {
                child.getValue(Task::class.java)?.let { taskList.add(it) }
            }
        }
        return taskList
    }

    suspend fun fetchReminders(): ArrayList<Reminder> {
        val reminderList = ArrayList<Reminder>()
        FirebaseUtils.auth.uid?.let { userId ->
            val snapshot = FirebaseUtils.database.child("reminders").child(userId).get().await()
            for (child in snapshot.children) {
                child.getValue(Reminder::class.java)?.let { reminderList.add(it) }
            }
        }
        return reminderList
    }
}

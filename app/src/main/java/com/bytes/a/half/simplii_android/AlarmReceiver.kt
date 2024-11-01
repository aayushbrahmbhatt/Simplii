package com.bytes.a.half.simplii_android

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat

class AlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        intent?.let {
            val taskTitle = it.getStringExtra(SimpliiConstants.KEY_TASK_TITLE)
            if (taskTitle.isValidString()) {
                displayNotification(context!!, taskTitle!!)
            }
        }
    }

    private fun displayNotification(context: Context, taskTitle: String) {
        val intent = Intent(context, AlarmReceiver::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent: PendingIntent =
            PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_IMMUTABLE)

        createNotificationChannel(context)

        val notificationBuilder = NotificationCompat.Builder(context, "TASK_NOTIFICATION")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle(context.getString(R.string.simplii_task_notification))
            .setContentText(taskTitle)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)

        with(NotificationManagerCompat.from(context)) {
            if (ActivityCompat.checkSelfPermission(
                    context,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                // TODO: Think about invoking
                //    ActivityCompat#requestPermissions
                // in this spot to ask for any required permissions that are missing. You should also
                //   override the method public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to manage the situation where the user approves the permission. Refer to the documentation
                // for ActivityCompat#requestPermissions for additional information.

                // Permission check for notifications. Handle as needed.
                return
            }
            notify(1, notificationBuilder.build())
        }
    }



    private fun createNotificationChannel(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channelName = "Task Notification"
            val channelDescription = "Channel for task reminders"
            val importance = NotificationManager.IMPORTANCE_HIGH
            val notificationChannel = NotificationChannel("TASK_NOTIFICATION", channelName, importance).apply {
                description = channelDescription
            }
            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(notificationChannel)
        }
    }
}

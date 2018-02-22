package com.example.clem3.carmonitor;

import android.net.Uri;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.util.Linkify;
import android.util.Log;
import android.view.WindowManager;
import android.webkit.WebView;
import android.widget.VideoView;

import com.erz.joysticklibrary.JoyStick;

/**
 * An example full-screen activity that shows and hides the system UI (i.e.
 * status bar and navigation/system bar) with user interaction.
 */
public class PilotActivity extends AppCompatActivity {
    int FORWARD = 1;
    int STOP = 0;
    int BACKWARD = -1;

    int CAMERA_MOVE_DELAY = 50;

    int previousAngle = 0;
    int previousSpeed = 0;
    int previousDirection = 0;
    long previousTimestamp = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_pilot);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.hide();
        }

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        JoyStick leftJoyStick = (JoyStick) findViewById(R.id.leftJoyStick);
        leftJoyStick.setListener(new JoyStick.JoyStickListener() {
            @Override
            public void onMove(JoyStick joyStick, double angle, double power, int direction) {
                Log.d("JoyStickGauche", "angle = " + angle + "angle = " + joyStick.getAngleDegrees() + " power = " + power + " direction = " + direction);
                GlobalClass globalVariable = (GlobalClass) getApplicationContext();
                if (power == 0)
                {
                    globalVariable.getClientThread().addRequest("setMotor", STOP);
                    previousDirection = STOP;
                }
                else
                {
                    int powerInt = (int) power;
                    if (Math.abs(powerInt - previousSpeed) > 5) {
                        globalVariable.getClientThread().addRequest("setSpeed", powerInt);
                        previousSpeed = powerInt;
                    }

                    //WARNING : angle = 0 -> (-1,0), angle = 180 -> (1,0)
                    int angleInt = (int) Math.abs(joyStick.getAngleDegrees());
                    if (Math.abs(angleInt - previousAngle) > 5) {
                        globalVariable.getClientThread().addRequest("setAngle", angleInt);
                        previousAngle = angleInt;
                    }

                    if (angle >= 0 && previousDirection != FORWARD) {
                        globalVariable.getClientThread().addRequest("setMotor", FORWARD);
                        previousDirection = FORWARD;
                    }
                    else if (angle < 0 && previousDirection != BACKWARD) {
                        globalVariable.getClientThread().addRequest("setMotor", BACKWARD);
                        previousDirection = BACKWARD;
                    }
                }

            }

            @Override
            public void onTap() {

            }

            @Override
            public void onDoubleTap() {

            }
        });

        JoyStick rightJoyStick = (JoyStick) findViewById(R.id.rightJoyStick);
        rightJoyStick.setListener(new JoyStick.JoyStickListener() {
            @Override
            public void onMove(JoyStick joyStick, double angle, double power, int direction) {
                Log.d("JoyStickDroit", "angle = " + angle + " power = " + power + " direction = " + direction);
                long newTimestamp = System.currentTimeMillis();
                if (direction != JoyStick.DIRECTION_CENTER && newTimestamp - previousTimestamp >= CAMERA_MOVE_DELAY){
                    previousTimestamp = newTimestamp;
                    GlobalClass globalVariable = (GlobalClass) getApplicationContext();
                    globalVariable.getClientThread().addRequest("moveCamera", direction);
                }
            }

            @Override
            public void onTap() {

            }

            @Override
            public void onDoubleTap() {
                GlobalClass globalVariable = (GlobalClass) getApplicationContext();
                globalVariable.getClientThread().addRequest("cameraHome");
            }
        });

        GlobalClass globalVariable = (GlobalClass) getApplicationContext();

        WebView web = (WebView) findViewById(R.id.webView);
        web.loadUrl("http://" + globalVariable.getServerAddress() + ":5000/video_feed");

    }
}

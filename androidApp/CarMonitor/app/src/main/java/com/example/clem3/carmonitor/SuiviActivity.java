package com.example.clem3.carmonitor;

import android.content.Intent;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebView;

public class SuiviActivity extends AppCompatActivity {

    private int speed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_suivi);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.hide();
        }

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        GlobalClass globalVariable = (GlobalClass) getApplicationContext();

        WebView web = (WebView) findViewById(R.id.webView);
        web.loadUrl("http://" + globalVariable.getServerAddress() + ":5000/video_feed");

//        VideoView view = (VideoView) findViewById(R.id.videoView);
//        view.setVideoPath("/sdcard/CR.mp4");
//        view.setVideoURI(Uri.parse("tcp/h264://192.168.43.75:8000"));
//        view.setVideoURI(Uri.parse("https://chaines-tv.orange.fr/#live/liveChannel/1401"));
//        view.start();
    }

    public void buttonStopHandler(View target){
        GlobalClass globalVariable = (GlobalClass) getApplicationContext();
        globalVariable.getClientThread().addRequest("stop");
    }

    public void buttonTargetHandler(View target){
        Intent intent = new Intent(this, ChooseTarget.class);
        startActivity(intent);
    }


}

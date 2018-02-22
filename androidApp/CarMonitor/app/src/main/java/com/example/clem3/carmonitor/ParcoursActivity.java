package com.example.clem3.carmonitor;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

public class ParcoursActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_parcours);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.hide();
        }

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        GlobalClass globalVariable = (GlobalClass) getApplicationContext();

        WebView web = (WebView) findViewById(R.id.webView);
        web.loadUrl("http://" + globalVariable.getServerAddress() + ":5000/video_feed");
    }

    public void buttonStopHandler(View target){
        GlobalClass globalVariable = (GlobalClass) getApplicationContext();
        globalVariable.getClientThread().addRequest("stop");
    }

    public void buttonCoordHandler(View target){
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Coordonnées");

        GridLayout layout = new GridLayout(this);
        layout.setRowCount(2);
        layout.setColumnCount(2);

        TextView latitudeTextView = new TextView(this);
        latitudeTextView.setText("Latitude :");
        GridLayout.LayoutParams lp = new GridLayout.LayoutParams();
        lp.rowSpec = GridLayout.spec(0,1);
        lp.columnSpec = GridLayout.spec(0,1);
        latitudeTextView.setLayoutParams(lp);
        layout.addView(latitudeTextView);

        final EditText latitude = new EditText(this);
        latitude.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);
        lp = new GridLayout.LayoutParams();
        lp.rowSpec = GridLayout.spec(0,1);
        lp.columnSpec = GridLayout.spec(1,1);
        lp.width = ViewGroup.LayoutParams.MATCH_PARENT;
        latitude.setLayoutParams(lp);
        layout.addView(latitude);

        TextView longitudeTextView = new TextView(this);
        longitudeTextView.setText("Longitude :");
        lp = new GridLayout.LayoutParams();
        lp.rowSpec = GridLayout.spec(1,1);
        lp.columnSpec = GridLayout.spec(0,1);
        longitudeTextView.setLayoutParams(lp);
        layout.addView(longitudeTextView);

        final EditText longitude = new EditText(this);
        longitude.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);
        lp = new GridLayout.LayoutParams();
        lp.rowSpec = GridLayout.spec(1,1);
        lp.columnSpec = GridLayout.spec(1,1);
        lp.width = ViewGroup.LayoutParams.MATCH_PARENT;
        longitude.setLayoutParams(lp);
        layout.addView(longitude);

        builder.setView(layout);
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                GlobalClass globalVariable = (GlobalClass) getApplicationContext();
                globalVariable.getClientThread().addRequest("setCoord", Double.parseDouble(latitude.getText().toString()), Double.parseDouble(longitude.getText().toString()));
            }
        });
        builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                dialogInterface.cancel();
            }
        });

        builder.show();
    }
}

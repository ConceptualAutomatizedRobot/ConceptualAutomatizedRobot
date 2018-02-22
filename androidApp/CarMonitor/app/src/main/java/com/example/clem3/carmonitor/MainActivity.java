package com.example.clem3.carmonitor;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import org.xmlrpc.android.XMLRPCClient;

import java.net.URI;

public class MainActivity extends AppCompatActivity {

    final int PILOT_MODE = 0;
    final int SUIVI_MODE = 1;
    final int PARCOURS_MODE = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void connectToCar()
    {
        EditText address = (EditText) findViewById(R.id.editTextAddress);
        EditText port = (EditText) findViewById(R.id.editTextPort);
        Log.d("URI", "http://" + address.getText() + ":" + port.getText());
        URI uri = URI.create("http://" + address.getText() + ":" + port.getText());
        GlobalClass globalVariable = (GlobalClass) getApplicationContext();
        XMLRPC_Thread clientThread = new XMLRPC_Thread(new XMLRPCClient(uri));
        clientThread.start();
        globalVariable.setClientThread(clientThread);
        globalVariable.setServerAddress(address.getText().toString());
    }

    public void buttonPilotHandler(View target){
        connectToCar();
        GlobalClass globalVariable = (GlobalClass) getApplicationContext();
        globalVariable.getClientThread().addRequest("setMode", PILOT_MODE);
        Intent intent = new Intent(this, PilotActivity.class);
        startActivity(intent);
    }

    public void buttonSuiviHandler(View target){
        connectToCar();
        GlobalClass globalVariable = (GlobalClass) getApplicationContext();
        globalVariable.getClientThread().addRequest("setMode", SUIVI_MODE);
        Intent intent = new Intent(this, SuiviActivity.class);
        startActivity(intent);
    }

    public void buttonParcoursHandler(View target){
        connectToCar();
        GlobalClass globalVariable = (GlobalClass) getApplicationContext();
        globalVariable.getClientThread().addRequest("setMode", PARCOURS_MODE);
        Intent intent = new Intent(this, ParcoursActivity.class);
        startActivity(intent);
    }
}

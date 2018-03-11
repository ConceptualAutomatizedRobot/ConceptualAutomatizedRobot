package com.example.clem3.carmonitor;

import android.app.AlertDialog;
import android.content.Context;
import android.content.CursorLoader;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.provider.MediaStore.Images;
import android.widget.ProgressBar;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

public class ChooseTarget extends AppCompatActivity implements XMLRPC_Thread.XMlRPC_Ack_Receiver {

    private final int SELECT_IMAGE = 1;

    Map<String, String> paths;

    int nbQrCodes = 0;
    String filePath;
    AlertDialog dialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choose_target);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_PICK, Images.Media.EXTERNAL_CONTENT_URI);
                intent.setType("image/*");
                startActivityForResult(intent, SELECT_IMAGE);
            }
        });

        /*SharedPreferences pref = getSharedPreferences("paths", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = pref.edit();
        editor.clear();
        editor.commit();*/

        paths = new HashMap<>();

        SharedPreferences pref = getSharedPreferences("paths", Context.MODE_PRIVATE);
        nbQrCodes = pref.getInt("nbQrCodes", 0);
        for (int i = 0 ; i < nbQrCodes ; ++i)
        {
            String name = pref.getString("" + i + "_name", "");
            String path = pref.getString("" + i + "_path", "");
            paths.put(name, path);
            LinearLayout layout = (LinearLayout) findViewById(R.id.linearLayout);
            Button b = getButton(name);
            layout.addView(b);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode)
        {
            case SELECT_IMAGE:
                if (resultCode == RESULT_OK)
                {
                    filePath = getRealPathFromURI(data.getData());

                    AlertDialog.Builder builder = new AlertDialog.Builder(this);
                    builder.setTitle("Target name");
                    final EditText input = new EditText(this);
                    builder.setView(input);
                    builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {

                            String name = input.getText().toString();

                            SharedPreferences pref = getSharedPreferences("paths", Context.MODE_PRIVATE);
                            SharedPreferences.Editor editor = pref.edit();
                            editor.putString("" + nbQrCodes + "_name", name);
                            editor.putString("" + nbQrCodes + "_path", filePath);
                            editor.putInt("nbQrCodes", ++nbQrCodes);
                            editor.commit();
                            paths.put(name, filePath);

                            final LinearLayout layout = (LinearLayout) findViewById(R.id.linearLayout);
                            Button b = getButton(name);
                            layout.addView(b);
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
                break;
        }
    }

    public Button getButton(String text)
    {
        Button b = new Button(getApplicationContext());
        b.setText(text);
        b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                GlobalClass globalVariable = (GlobalClass) getApplicationContext();

                AlertDialog.Builder builder = new AlertDialog.Builder(ChooseTarget.this);
                builder.setTitle("Sending File");
                ProgressBar progressBar = new ProgressBar(ChooseTarget.this);
                builder.setView(progressBar);
                builder.setCancelable(false);
                dialog = builder.show();

                globalVariable.getClientThread().addRequestWithAck("setTarget", fileToBytes(paths.get(((Button) view).getText().toString())), ChooseTarget.this);
            }
        });

        return b;
    }

    static public byte[] fileToBytes(String path)
    {
        File file = new File(path);
        //init array with file length
        byte[] bytesArray = new byte[(int) file.length()];

        FileInputStream fis;
        try {
            fis = new FileInputStream(file);
            fis.read(bytesArray); //read file into bytes[]
            fis.close();
            return bytesArray;
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    public String getRealPathFromURI(Uri contentUri) {
        String[] proj = { MediaStore.Images.Media.DATA };

        CursorLoader cursorLoader = new CursorLoader(this, contentUri, proj, null, null, null);
        Cursor cursor = cursorLoader.loadInBackground();

        int column_index =
                cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        cursor.moveToFirst();
        return cursor.getString(column_index);
    }

    @Override
    public void XMlRPC_Ack(Object result) {
        dialog.dismiss();
    }
}

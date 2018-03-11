package com.example.clem3.carmonitor;

import android.app.Application;

import org.xmlrpc.android.XMLRPCClient;

import java.net.URI;

/**
 * Created by clem3 on 03/02/2018.
 */

public class GlobalClass extends Application {
    private String serverAddress;
    private XMLRPC_Thread clientThread;

    public String getServerAddress() {
        return serverAddress;
    }

    public void setServerAddress(String serverAddress) {
        this.serverAddress = serverAddress;
    }

    public XMLRPC_Thread getClientThread() {
        return clientThread;
    }

    public void setClientThread(XMLRPC_Thread clientThread) {
        this.clientThread = clientThread;
    }

}

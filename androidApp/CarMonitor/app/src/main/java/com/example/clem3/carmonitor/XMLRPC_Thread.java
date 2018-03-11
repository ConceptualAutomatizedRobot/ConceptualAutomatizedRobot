package com.example.clem3.carmonitor;

import android.util.Log;
import android.util.Pair;

import org.xmlrpc.android.XMLRPCClient;
import org.xmlrpc.android.XMLRPCException;

import java.util.LinkedList;
import java.util.Queue;

/**
 * Created by clem3 on 03/02/2018.
 */

public class XMLRPC_Thread extends Thread{

    public interface XMlRPC_Ack_Receiver {
        void XMlRPC_Ack(Object result);
    }

    public class Triple<X, Y, Z>{
        public X first;
        public Y second;
        public Z third;

        public Triple(X first, Y second, Z third) {
            this.first = first;
            this.second = second;
            this.third = third;
        }
    }

    private Object synchro;
    private XMLRPCClient client;
    private Queue<Triple<String, Object[], XMlRPC_Ack_Receiver>> queue;

    private boolean connectionClosed;

    public XMLRPC_Thread(XMLRPCClient client) {
        this.synchro = new Object();
        this.client = client;
        this.queue = new LinkedList<>();
        this.connectionClosed = false;
    }

    @Override
    public void run() {
        while (!connectionClosed)
        {
            while (!queue.isEmpty())
            {
                Triple<String, Object[], XMlRPC_Ack_Receiver> triple;
                synchronized (synchro)
                {
                    triple = queue.poll();
                }
                try {
                    Object result = client.callEx(triple.first, triple.second);
                    if (triple.third != null)
                    {
                        triple.third.XMlRPC_Ack(result);
                    }
                } catch (XMLRPCException e) {
                    e.printStackTrace();
                }
            }
            synchronized (synchro)
            {
                if (queue.isEmpty())
                {
                    try {
                        synchro.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }

    void addRequest(final String method, final Object[] params, final XMlRPC_Ack_Receiver asker)
    {
        synchronized (synchro)
        {
            queue.add(new Triple<>(method, params, asker));
            synchro.notify();
        }
    }

    void addRequest(final String method, final Object[] params) { addRequest(method, params, null); }

    void addRequest(final String method, final Object param1, final Object param2)
    {
        Object[] params = {param1, param2};
        addRequest(method, params);
    }

    void addRequest(final String method, final Object param)
    {
        Object[] params = {param};
        addRequest(method, params);
    }

    void addRequest(final String method)
    {
        addRequest(method, null);
    }

    void addRequestWithAck(final String method, final Object param, final XMlRPC_Ack_Receiver asker)
    {
        Object[] params = {param};
        addRequest(method, params, asker);
    }

    void closeConnection()
    {
        synchronized (synchro)
        {
            connectionClosed = true;
            synchro.notify();
        }
    }
}

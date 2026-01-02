/*
frontend/js/websocket_client.js

This script handles the WebSocket connection to the backend.
It receives real-time pose data and passes it to the SkeletonVisualizer.
*/

class WebSocketClient {
    constructor(url, onMessageCallback) {
        this.url = url;
        this.onMessageCallback = onMessageCallback;
        this.socket = null;
    }

    connect() {
        console.log("Connecting to WebSocket...");
        // this.socket = new WebSocket(this.url);
        
        // TODO: Handle onopen, onmessage, onerror, onclose
        // this.socket.onmessage = (event) => {
        //     const data = JSON.parse(event.data);
        //     this.onMessageCallback(data);
        // };
    }
}

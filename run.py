from social_network import app, socketio


if __name__ == '__main__':
    
    socketio.run(app, debug=True, ssl_context=('cert.pem', 'key.pem'))
    
    
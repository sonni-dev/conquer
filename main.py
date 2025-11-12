from app import app

if __name__ == '__main__':
    print("\n🗡️ Conquer Started!")
    print("📍 Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
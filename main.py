import peer

# Example usage:
if __name__ == "__main__":
    node1 = Peer("0.0.0.0", 8000)
    node1.start()

    node2 = Peer("0.0.0.0", 8001)
    node2.start()

    # Give some time for nodes to start listening
    import time
    time.sleep(2)

    node2.connect("127.0.0.1", 8000)
    time.sleep(1)  # Allow connection to establish
    node2.send_data("Hello from node2!")

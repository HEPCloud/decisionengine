"""
Source Subscription Manager
"""

import collections
import multiprocessing
import queue
import threading
import time


class Subscription:
    # Subscriptions are used as an abstraction of all the information required by the SourceSubscriptionManager to bind a Channel to its Sources
    def __init__(self, channel_manager_id, channel_manager_name, source_names):
        self.channel_manager_id = channel_manager_id
        self.channel_manager_name = channel_manager_name
        self.sources = source_names


class SourceSubscriptionManager(threading.Thread):
    """
    This implements the communication between Sources and Channels
    """

    def __init__(self):
        super().__init__()
        self.keep_running = multiprocessing.Value("i", 1)
        self.data_product_queue = multiprocessing.Queue()  # Incoming data blocks from source processes
        self.subscribe_queue = multiprocessing.Queue()  # Incoming source subscriptions by channels

        self.manager = multiprocessing.Manager()
        self.channel_subscribed = self.manager.dict()  # Notify channel when subscription process has completed

        self.source_subscriptions = collections.defaultdict(
            list
        )  # Map sources to a list of channel ids subscribed to those sources
        self.sources = collections.defaultdict(list)  # Map sources to lists of source ids

        self.channel_data_sinks = collections.defaultdict(
            multiprocessing.Queue
        )  # Maintain an multiprocessing Queue for each channel to have data products communicated to it

    def get_new_subscriptions(self):
        # This thread should construct the datablocks for the channels and manage the source content within them for a channel.i
        #   This prevents us from having to communicate anything more complex than Python builtin classes accross process boundaries.
        try:
            new_subscription = self.subscribe_queue.get(block=False)
            sub_id = new_subscription.channel_manager_id

            for source in new_subscription.sources:
                self.source_subscriptions[source].append(sub_id)
        except queue.Empty:
            pass
        else:
            self.channel_subscribed[sub_id] = True

    def send_data_product_to_subscribed(self, new_source_info):
        # Send data product to the channels that are subscribed to the source that generated it
        source_name = new_source_info["source_name"]
        for channel_id in self.source_subscriptions[source_name]:
            self.channel_data_sinks[channel_id].append(new_source_info)

    def run(self):
        while self.keep_running:
            self.get_new_subscriptions()
            try:
                # Check for new data blocks
                # source_new_info = { 'source_name': source_name, 'source_id': source_id , 'data': data, 'header': header }
                new_source_info = self.data_product_queue.get(timeout=1)
            except queue.Empty:
                time.sleep(1)
            else:
                self.send_data_product_to_subscribed(new_source_info)

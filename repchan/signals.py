# -*- encoding: utf-8
import types

from django.dispatch import Signal


def signal_id(instance, signal_object):
    'returns the signal id'
    return (id(instance), id(signal_object))


def signal_send_on(instance, signal_object):
    'Enable sending a signal'
    instance._signal_disable.remove(signal_id(instance, signal_object))


def signal_send_off(instance, signal_object):
    '''
    Disable sending a signal
    
    instance - current object instance
    signal_object - object type Signal
    '''
    try:
        instance._signal_disable.append(signal_id(instance, signal_object))
    except AttributeError:
        instance._signal_disable = [signal_id(instance, signal_object)]


def signal_send_status(instance, signal_object):
    '''
    Checking the status of the signal. 
    
    True if the signal can be sent, otherwise false.
    '''
    try:
        return not signal_id(instance, signal_object) in\
                                    instance._signal_disable
    except KeyError:
        return True

def signal_resend(instance, signal_object):
    'Resend signal from buffer'
    signal_buffer_clear(instance, signal_object)


def signal_allow(instance, signal_object, count=1):
    'Allow you to send a signal "count" times'
    sid = signal_id(instance, signal_object)
    try:
        instance._signal_allow[sid] = count
    except (KeyError, AttributeError):
        instance._signal_allow = { sid:count }


def signal_allow_check(instance, signal_object, decrement=False):
    'Check that the signal can be sent.'
    sid = signal_id(instance, signal_object)
    try:
        if instance._signal_allow[sid]:
            if decrement:
                instance._signal_allow[sid] -= 1
            return True
    except (KeyError, AttributeError):
        return False

def signal_send_mask(signal_object):
    'Decorator that masks blocked signals.'
    send_oryginal = signal_object.send

    def send(self, sender, **named):
        try:
            # skip if the signal does not have a parameter with
            # an instance of an object
            instance = named['instance']
            sid = signal_id(instance, signal_object)
            if signal_allow_check(instance, signal_object, decrement=True):
                return send_oryginal(sender, **named)
            # If the signal is blocked, do not send notifications.
            if sid in instance._signal_disable:
                return
        except (KeyError, AttributeError):
            return send_oryginal(sender, **named)

    signal_object.send = types.MethodType(send, signal_object, signal_object.__class__)



# Signls
revision_post_commit = Signal(providing_args=["instance", "using"])
revision_post_create = Signal(providing_args=["instance", "using"])
revision_set_as_main = Signal(providing_args=["instance", "using"])


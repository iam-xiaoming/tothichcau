from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from django.utils import timezone

# Create your views here.

def human_readable_time_ago(timestamp):
    now = timezone.now()
    diff = now - timestamp

    if diff.days >= 1:
        return f"{diff.days} days ago"
    else:
        hours = diff.seconds // 3600
        if hours >= 1:
            return f"{hours} hours ago"
        else:
            minutes = diff.seconds // 60
            if minutes >= 1:
                return f"{minutes} minutes ago"
            else:
                return "Just now"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    try:
        notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')
    except Notification.DoesNotExist:
        return Response({'error': 'Notification does not exists.'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
    data = [
        {
            'sender': n.sender.username,
            'message': n.message,
            'timestamp': human_readable_time_ago(n.timestamp),
        }
        for n in notifications
    ]
    
    return Response({'success': True, 'notifications': data, 'message': 'Fetch notifications successfully'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    try:
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification does not exists.'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
    return Response({'success': True, 'message': 'Mark as read successfully.'}, status=200)
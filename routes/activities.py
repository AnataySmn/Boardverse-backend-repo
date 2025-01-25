import uuid
from flask import Blueprint, jsonify, request
from models.activity import Activity
from extensions import db
from datetime import datetime

activity_blueprint = Blueprint('activity', __name__)

# Get all activities for a user
@activity_blueprint.route('/activities/<userId>', methods=['GET'])
def get_activities(userId):
    activities = Activity.query.filter_by(userId=userId).all()
    if activities:
        activity_list = [{
            'activityId': activity.activityId,
            'gameName': activity.gameName,
            'duration': activity.duration,
            'result': activity.result,
            'rankChange': activity.rankChange,
            'playedAt': activity.playedAt
        } for activity in activities]
        return jsonify(activity_list), 200
    else:
        return jsonify({'error': 'No activities found for this user'}), 404

# Add a new activity for a user
@activity_blueprint.route('/activities', methods=['POST'])
def add_activity():
    data = request.json
    user_id = data.get('userId')

    new_activity = Activity(
        activityId=str(uuid.uuid4()),
        userId=user_id,
        gameName=data.get('gameName'),
        duration=data.get('duration', 0),
        result=data.get('result', 'Pending'),
        rankChange=data.get('rankChange', 0),
        playedAt=data.get('playedAt', datetime.utcnow())
    )

    try:
        db.session.add(new_activity)
        db.session.commit()
        return jsonify({'message': 'Activity added successfully!', 'activityId': new_activity.activityId}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing activity
@activity_blueprint.route('/activities/<activityId>', methods=['PUT'])
def update_activity(activityId):
    data = request.json
    activity = Activity.query.filter_by(activityId=activityId).first()

    if activity:
        try:
            activity.gameName = data.get('gameName', activity.gameName)
            activity.duration = data.get('duration', activity.duration)
            activity.result = data.get('result', activity.result)
            activity.rankChange = data.get('rankChange', activity.rankChange)
            activity.playedAt = data.get('playedAt', activity.playedAt)

            db.session.commit()
            return jsonify({'message': 'Activity updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Activity not found'}), 404

# Delete an activity
@activity_blueprint.route('/activities/<activityId>', methods=['DELETE'])
def delete_activity(activityId):
    activity = Activity.query.filter_by(activityId=activityId).first()

    if activity:
        try:
            db.session.delete(activity)
            db.session.commit()
            return jsonify({'message': 'Activity deleted successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Activity not found'}), 404

import uuid
from flask import Blueprint, jsonify, request
from models.stats import Stats
from extensions import db

stats_blueprint = Blueprint('stats', __name__)

# Get stats for a user
@stats_blueprint.route('/stats/<userId>', methods=['GET'])
def get_stats(userId):
    stats = Stats.query.filter_by(userId=userId).first()
    if stats:
        return jsonify({
            'totalGamesPlayed': stats.totalGamesPlayed,
            'totalWins': stats.totalWins,
            'totalLosses': stats.totalLosses,
            'rankScore': stats.rankScore
        }), 200
    return jsonify({'error': 'Stats not found'}), 404

# Update stats for a user
@stats_blueprint.route('/stats/<userId>', methods=['PUT'])
def update_stats(userId):
    data = request.json
    stats = Stats.query.filter_by(userId=userId).first()

    if stats:
        try:
            stats.totalGamesPlayed = data.get('totalGamesPlayed', stats.totalGamesPlayed)
            stats.totalWins = data.get('totalWins', stats.totalWins)
            stats.totalLosses = data.get('totalLosses', stats.totalLosses)
            stats.rankScore = data.get('rankScore', stats.rankScore)

            db.session.commit()
            return jsonify({'message': 'Stats updated successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Stats not found'}), 404

# Create stats for a user (in case of manual creation, e.g., admin action)
@stats_blueprint.route('/stats', methods=['POST'])
def create_stats():
    data = request.json
    user_id = data.get('userId')

    if Stats.query.filter_by(userId=user_id).first():
        return jsonify({'error': 'Stats already exist for this user'}), 400

    new_stats = Stats(
        statsID=str(uuid.uuid4()),
        userId=user_id,
        totalGamesPlayed=data.get('totalGamesPlayed', 0),
        totalWins=data.get('totalWins', 0),
        totalLosses=data.get('totalLosses', 0),
        rankScore=data.get('rankScore', 0)
    )

    try:
        db.session.add(new_stats)
        db.session.commit()
        return jsonify({'message': 'Stats created successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete stats for a user (if necessary for cleanup purposes)
@stats_blueprint.route('/stats/<userId>', methods=['DELETE'])
def delete_stats(userId):
    stats = Stats.query.filter_by(userId=userId).first()

    if stats:
        try:
            db.session.delete(stats)
            db.session.commit()
            return jsonify({'message': 'Stats deleted successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Stats not found'}), 404

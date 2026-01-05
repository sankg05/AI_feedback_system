import os
from flask import request, jsonify
from app import app
from app.db import SessionLocal
from app.models import Review

def serialize_review(review):
    return {
        "id": review.id,
        "rating": review.rating,
        "review_text": review.review_text,
        "ai_user_response": review.ai_user_response,
        "ai_summary": review.ai_summary,
        "ai_recommended_actions": review.ai_recommended_actions,
        "status": review.status,
        "error_message": review.error_message,
        "created_at": review.created_at.isoformat()
    }

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/api/review", methods=["POST"])
def submit_review():
    data = request.get_json()

    rating = data.get("rating")
    review_text = data.get("review", "")

    if not rating or rating < 1 or rating > 5:
        return jsonify({"error": "Invalid rating"}), 400

    db = SessionLocal()
    try:
        review = Review(
            rating=rating,
            review_text=review_text
        )
        db.add(review)
        db.commit()
        db.refresh(review)
    finally:
        db.close()

    return jsonify({"success": True, "review_id": review.id})

@app.route("/api/admin/reviews", methods=["GET"])
def fetch_all_reviews():
    db = SessionLocal()
    try:
        reviews = db.query(Review).order_by(Review.created_at.desc()).all()
        serialized_reviews = [serialize_review(r) for r in reviews]
    finally:
        db.close()

    return jsonify({
        "count": len(serialized_reviews),
        "reviews": serialized_reviews
    })
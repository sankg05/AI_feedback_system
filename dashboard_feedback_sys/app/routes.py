import os
from flask import request, jsonify, render_template
from app import app
from app.db import SessionLocal
from app.models import Review
from app.llm import process_review_with_gemini

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

@app.route("/")
def user_dashboard():
    return render_template("user.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")

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

    llm_result = process_review_with_gemini(rating, review_text)

    db = SessionLocal()
    try:
        review = Review(
            rating=rating,
            review_text=review_text,
            ai_user_response=llm_result["user_response"],
            ai_summary=llm_result["summary"],
            ai_recommended_actions=llm_result["recommended_actions"],
            status=llm_result["status"],
            error_message=llm_result["error"]
        )

        db.add(review)
        db.commit()
        db.refresh(review)

    except Exception as e:
        db.rollback()
        return jsonify({"error": "Failed to store review"}), 500

    finally:
        db.close()

    return jsonify({
        "success": True,
        "ai_response": llm_result["user_response"]
    })

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
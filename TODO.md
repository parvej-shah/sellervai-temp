1. Order config not available in store page - like what infos to include checklist
2. NEXT test connecting different page. Like from product page to cart page.
3. currently we have short time token, getting expired.. we should to long living access token. users wont login everyday..


curl -X POST "https://graph.facebook.com/v25.0/<post_id>/comments" \
  -d "message=test comment from api" \
  -d "access_token=EAANuWyN3n0EBRhlFtAn8FOkLZCTMW6vo2HvQb1sVZBraVRTybocjee5ZA1Ve8IBYcgGkGWpz7cOguPFLLclxL9N66qI6gM6z9I9H5UtUlBYMxAAxRBAk4GhGkIwfQEc3FT8ZClZBJ6ZBeWyYLDkQzbtIA5WZB2cywFh75X746mQhbx4yhwNYpYBUNNTfjOLxyjxg0ZBi"

curl "https://graph.facebook.com/v25.0/?id=https://www.facebook.com/permalink.php?story_fbid=pfbid0EzLbYncWMCA9tZtk4Rd2YN9Y2YQ6C1SJBcWwN9WDpq7NJkiswg2ef8jjV5n5syLrl%26id=61582042883677&access_token=EAANuWyN3n0EBRhlFtAn8FOkLZCTMW6vo2HvQb1sVZBraVRTybocjee5ZA1Ve8IBYcgGkGWpz7cOguPFLLclxL9N66qI6gM6z9I9H5UtUlBYMxAAxRBAk4GhGkIwfQEc3FT8ZClZBJ6ZBeWyYLDkQzbtIA5WZB2cywFh75X746mQhbx4yhwNYpYBUNNTfjOLxyjxg0ZBi&fields=id"



curl -X POST "https://graph.facebook.com/v25.0/61582042883677/subscribed_apps" \
  -d "subscribed_fields=feed,group_feed,messages,messaging_postbacks" \
  -d "access_token=EAANuWyN3n0EBRhlFtAn8FOkLZCTMW6vo2HvQb1sVZBraVRTybocjee5ZA1Ve8IBYcgGkGWpz7cOguPFLLclxL9N66qI6gM6z9I9H5UtUlBYMxAAxRBAk4GhGkIwfQEc3FT8ZClZBJ6ZBeWyYLDkQzbtIA5WZB2cywFh75X746mQhbx4yhwNYpYBUNNTfjOLxyjxg0ZBi"

curl "https://graph.facebook.com/v25.0/me/accounts?fields=id,name,access_token&access_token=EAANuWyN3n0EBRhlFtAn8FOkLZCTMW6vo2HvQb1sVZBraVRTybocjee5ZA1Ve8IBYcgGkGWpz7cOguPFLLclxL9N66qI6gM6z9I9H5UtUlBYMxAAxRBAk4GhGkIwfQEc3FT8ZClZBJ6ZBeWyYLDkQzbtIA5WZB2cywFh75X746mQhbx4yhwNYpYBUNNTfjOLxyjxg0ZBi"
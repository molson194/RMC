Action Items
* Redirect to non-callback url
* Three tabs: my reviews, give new review, given reviews
* On any request, validate the access token. 
  * If expired access token or does not exist, validate refresh token
  * If expired refresh token or does not exist, sign out the user
  * If valid refresh token, generate new access token and set cookie

Advice for Static Web App Team
* Function logs by default (create AppInsights and link)
* Click function to view content
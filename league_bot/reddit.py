import praw
import watcher

from league_bot.credentials import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT


def main():
    """Run the script."""
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         username=USERNAME,
                         password=PASSWORD,
                         user_agent=USER_AGENT)

    rbots = reddit.subreddit("rbots")

    for comment in rbots.stream.comments():
        process_comment(comment)


def process_comment(comment):
    """Process an incoming comment."""
    call_out = "/u/NotASmartBot"
    if comment.body.startswith(call_out) and "free rotation" in comment.body:
        comment.refresh()
        if USERNAME in [c.author.name for c in comment.replies.list()]:
            return
        free_champs = watcher.get_free_champs(watcher.watcher)
        comment.reply(f"Free rotation: {', '.join(free_champs)}")
        print("Replied to a comment.")


if __name__ == '__main__':
    main()

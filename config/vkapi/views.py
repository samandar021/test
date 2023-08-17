from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Post
from .serializers import ProfileSerializer, PostSerializer


class ProfileViewD(APIView):
    def get(self, request):
        profile_id = request.GET.get('profile')
        try:
            profile = Profile.objects.get(profile_id=profile_id)
            serializer = ProfileSerializer(profile)
            return Response({"status": "success", "code": 200, "data": serializer.data})
        except Profile.DoesNotExist:
            return Response({"status": "error", "code": 403, "message": "Invalid account name"})


class LikesViewD(APIView):
    def get(self, request):
        link = request.GET.get('link')
        try:
            post = Post.objects.get(url=link)
            serializer = PostSerializer(post)
            return Response({"status": "success", "code": 200, "data": serializer.data})
        except Post.DoesNotExist:
            return Response({"status": "error", "code": 403, "message": "Invalid account name"})


class ProfileView(APIView):
    def get(self, request):
        profile_id = request.GET.get('profile')

        # Make a request to VK's public profile API
        vk_profile_url = f"https://api.vk.com/method/users.get?user_ids={profile_id}&fields=photo_200,followers_count,counters&v=5.130"
        response = requests.get(vk_profile_url)
        data = response.json()

        if "error" in data:
            return Response({"status": "error", "code": 403, "message": "Invalid account name"})

        profile_data = data["response"][0]
        serializer_data = {
            "profile_id": profile_data["id"],
            "avatar_url": profile_data.get("photo_200", ""),
            "followers": profile_data.get("followers_count", ""),
            "following": profile_data["counters"].get("friends", ""),
        }

        return Response({"status": "success", "code": 200, "data": serializer_data})


class LikesView(APIView):
    def get(self, request):
        link = request.GET.get('link')

        # Extract the post_id from the link
        post_id = link.split('/')[-1]

        # Make a request to VK's public post likes API
        vk_post_url = f"https://api.vk.com/method/likes.getList?type=post&item_id={post_id}&v=5.130"
        vk_post_response = requests.get(vk_post_url)
        vk_post_data = vk_post_response.json()

        if "error" in vk_post_data:
            return Response({"status": "error", "code": 403, "message": "Invalid post link"})

        # Fetching share and views using VK's wall.getById API
        vk_wall_url = f"https://api.vk.com/method/wall.getById?posts={post_id}&v=5.130"
        vk_wall_response = requests.get(vk_wall_url)
        vk_wall_data = vk_wall_response.json()

        if "error" in vk_wall_data:
            return Response({"status": "error", "code": 403, "message": "Invalid post link"})

        post_data = vk_wall_data["response"][0]
        likes_count = vk_post_data["response"]["count"]
        share_count = post_data.get("reposts", {}).get("count", "")
        views_count = post_data.get("views", {}).get("count", "")

        return Response({
            "status": "success",
            "code": 200,
            "data": {
                "post_id": post_id,
                "url": link,
                "likes": str(likes_count),
                "share": str(share_count),
                "views": str(views_count)
            }
        })


import requests
from rest_framework.views import APIView
from rest_framework.response import Response


class PostsListView(APIView):
    def get(self, request):
        profile_id = request.GET.get('profile')

        # Make a request to VK's public profile API to get user_id
        vk_profile_url = f"https://api.vk.com/method/users.get?user_ids={profile_id}&v=5.130"
        response = requests.get(vk_profile_url)
        data = response.json()

        if "error" in data:
            return Response({"status": "error", "code": 403, "message": "Invalid account name"})

        user_id = data["response"][0]["id"]

        # Make a request to VK's public wall.get API to get the last 10 posts
        vk_wall_url = f"https://api.vk.com/method/wall.get?owner_id={user_id}&count=10&v=5.130"
        response = requests.get(vk_wall_url)
        data = response.json()

        if "error" in data:
            return Response({"status": "error", "code": 403, "message": "Error fetching posts"})

        posts = []
        for post in data["response"]["items"]:
            post_id = f"{user_id}_{post['id']}"
            post_url = f"https://vk.com/wall{post_id.split('_')[0]}_{post_id.split('_')[1]}"
            post_likes = post.get("likes", {}).get("count", "")
            post_shares = post.get("reposts", {}).get("count", "")
            post_views = post.get("views", {}).get("count", "")

            posts.append({
                "post_id": post_id,
                "url": post_url,
                "likes": str(post_likes),
                "share": str(post_shares),
                "views": str(post_views)
            })

        # Fetch likes and other metrics of the last post
        if posts:
            last_post_id = posts[0]["post_id"].split('_')[1]
            vk_post_url = f"https://api.vk.com/method/likes.getList?type=post&item_id={last_post_id}&v=5.130"
            vk_post_response = requests.get(vk_post_url)
            vk_post_data = vk_post_response.json()

            if "error" in vk_post_data:
                return Response({"status": "error", "code": 403, "message": "Error fetching post likes"})

            last_post_likes = vk_post_data["response"]["count"]
            # Fetch other metrics for the last post using VK's wall.getById API
            vk_wall_url = f"https://api.vk.com/method/wall.getById?posts={last_post_id}&v=5.130"
            vk_wall_response = requests.get(vk_wall_url)
            vk_wall_data = vk_wall_response.json()

            if "error" in vk_wall_data:
                return Response({"status": "error", "code": 403, "message": "Error fetching post metrics"})

            last_post = posts[0]
            last_post["likes"] = str(last_post_likes)
            last_post["share"] = str(vk_wall_data["response"][0].get("reposts", {}).get("count", ""))
            last_post["views"] = str(vk_wall_data["response"][0].get("views", {}).get("count", ""))

        # Make a request to VK's public profile API to get avatar URL and other info
        vk_profile_url = f"https://api.vk.com/method/users.get?user_ids={user_id}&fields=photo_200&v=5.130"
        response = requests.get(vk_profile_url)
        data = response.json()

        profile_data = data["response"][0]

        serializer_data = {
            "profile_id": user_id,
            "avatar_url": profile_data.get("photo_200", ""),
            "posts": posts
        }

        return Response({"status": "success", "code": 200, "data": serializer_data})

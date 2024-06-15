function deleteProfilePicture() {
    if (confirm("Are you sure you want to delete your profile picture?")) {
        window.location.href = "{% url 'delete_profile_picture' %}";
    }
}

function uploadProfilePicture() {
    document.getElementById('profilePictureForm').submit();
}
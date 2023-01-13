// make redirect is searched product not found
setTimeout(function () {
    window.location.href = "{% url '404' %}";
});
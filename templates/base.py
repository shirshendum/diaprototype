<!DOCTYPE html>
<html>
<head>
    <title>Your Website</title>
</head>
<body>
    <header>
        <div id="website-name">Your Website</div>
        <!-- Logout button -->
        <form action="/logout" method="GET">
            <button type="submit">Logout</button>
        </form>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>


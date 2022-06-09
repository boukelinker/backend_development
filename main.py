# Do not modify these lines
__winc_id__ = '7b9401ad7f544be2a23321292dd61cb6'
__human_name__ = 'arguments'

# Add your code after this line

# 1 Greet template -------------------------------------------------------------------------------------------------------------------------


def greet(name, greeting_template="Hello, <name>!"):
    greeting = greeting_template.replace('<name>', name)
    return greeting


print(greet('Jan'))
print(greet('Jan', 'Whats up, <name>!'))

# 2 Force -------------------------------------------------------------------------------------------------------------------------


def force(mass, body='earth'):
    if body in planets:
        g = planets[body]
        F = mass * g
        return F
    else:
        return 'Planet is not in the list of planets'


planets = {
    'sun': 274,
    'jupiter': 24.9,
    'neptune': 11.2,
    'saturn': 10.4,
    'earth': 9.8,
    'uranus': 8.9,
    'venus': 8.9,
    'mars': 3.7,
    'mercury': 3.7,
    'moon': 1.6,
    'pluto': 0.6
}

print(force(mass=10, body='uranus'))

# 3 Gravity -------------------------------------------------------------------------------------------------------------------------


def pull(m1, m2, d):
    G = 6.674*10**-11       # --> Gravitational constant
    F = G*((m1*m2)/d**2)
    return F


print(pull(m1=0.1, m2=5.972*10**24, d=6.371*10**6))

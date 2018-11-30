# I cheated
# Requires selenium 

from contextlib import contextmanager
from scipy import stats

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys


def main():
    ## Load the page
    # Setup selenium chrome browser
    # driver = webdriver.Chrome("lib/chromedriver")
    driver = webdriver.Firefox(executable_path="lib/geckodriver")
    # Load a page so we can set cookies
    driver.get("http://guessthecorrelation.com/")

    print("When you've started the game, press enter")
    input()

    # Wait for page load
    try:
        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'nv-group')
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        raise
    print("Running...")

    while True:
        # Find element containing points
        container = driver.find_elements(By.CLASS_NAME, "nv-group")[0]
        html_points = container.find_elements_by_xpath(".//*")

        # Grab location of all points
        points_x = []
        points_y = []
        for html_point in html_points:
            matrix = html_point.get_property("transform")['animVal']['0']['matrix']
            x = matrix['e']
            y = matrix['f']
            points_x.append(int(x))
            points_y.append(int(y))

        # Calculate r
        slope, intercept, r_value, p_value, std_err = stats.linregress(points_x,points_y)
        r_value = abs(round(r_value, 4))
        print(r_value)

        # Enter answer
        answer_box = driver.find_element_by_id("guess-input")
        answer_box.click()
        answer_box.send_keys(Keys.BACKSPACE) # Remove 0. that starts in box
        answer_box.send_keys(Keys.BACKSPACE)
        answer_box.send_keys(str(r_value))
        answer_box.send_keys(Keys.ENTER)

        # Click next
        next_button = driver.find_element_by_id("next-btn")
        next_button.click()



if __name__ == '__main__':
    main()
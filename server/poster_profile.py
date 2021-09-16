import profile

import dao
import poster


def profileTest():

    for i in range(30):
        code = '5b0b06feeb582fdce2973a4ae227b2f0'
        data = dao.find_share_data(code)
        buf, mimetype = poster.drawio(data)


if __name__ == "__main__":
    profile.run("profileTest()")

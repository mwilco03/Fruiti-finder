#credit to HashGrind
import sys
import GoogleMapsQueryArgsDeserializer


def run():
    test_data = [
        '!3m1!4b1!4m5!3m4!1s0x54d13f95770661ab:0xc4447dd6cc95e535!8m2!3d41.12361!4d-124.15556'
    ]

    helper = GoogleMapsQueryArgsDeserializer.GoogleMapsQueryArgsDeserializer()

    for t in test_data:
        print(t)
        print(helper.deserialize(t))

    return 0


if __name__ == '__main__':
    sys.exit(run())

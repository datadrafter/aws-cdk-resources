from aws_cdk import App, Tags, Environment
from images_cdn.images_cdn_stack import ImagesCdnStack



images_cdn = ImagesCdnStack(app, 
                    id="images-cdn",
                    env=Environment(region='us-east-1'),
                    bucket_name="images.sbhat.me",
                    cf_id="cf_cdn")
Tags.of(images_cdn).add("used_for", "Blog images")
Tags.of(images_cdn).add("created_by", "sathyabhat")

cpgweds_cdn = ImagesCdnStack(app, 
                    id="cpgweds", 
                    env=Environment(region='us-east-1'),
                    bucket_name="joshenoy.weds.sathyabh.at",
                    cf_id="cpgweds_cf")
Tags.of(cpgweds_cdn).add("used_for", "cpgweds.com site")
Tags.of(cpgweds_cdn).add("created_by", "sathyabhat")

all_images_cdn = ImagesCdnStack(app, 
                    id="all-images",
                    env=Environment(region='us-east-1'),
                    bucket_name="i.sathyabh.at",
                    cf_id="cf_cdn")

Tags.of(all_images_cdn).add("used_for", "Blog images")
Tags.of(all_images_cdn).add("created_by", "sathyabhat")
